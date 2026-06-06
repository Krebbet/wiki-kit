---
name: self-play-theorem-proving-theory
description: Chen & Li 2026 (arXiv:2606.01861) — theoretical framework for prover-conjecturer self-play in formal theorem proving. Formalises theorems as a semantic graph, proves exponential proved-set growth under reversible random-walk conjecturing on well-connected graphs, and proposes a diffusion-similarity diversity measure (computed via contrastive embedding) to counter the empirical pathology of artificially complex, non-fundamental conjectures.
type: research
---

# A Theoretical Framework for Self-Play Theorem Proving Algorithms

Thomas Chen, Zhiyuan Li. arXiv:2606.01861 [cs.LG], 1 Jun 2026. A theoretical companion to empirical prover-conjecturer self-play systems (building on Dong & Ma 2025). The paper formalises the theorem space as a graph with edges between semantically similar theorems, proves that reversible-random-walk conjecturing on a well-connected graph suffices for *exponential* growth of the proved theorem set, and diagnoses and addresses the canonical empirical failure mode — conjecturer collapse to complex, non-fundamental theorems — via a diffusion-similarity diversity measure computed through contrastive learning.

## Method

### Theorem graph

Theorems are nodes in a graph $\mathcal{G} = (V, E)$; an edge $(u, v) \in E$ iff $u$ and $v$ are *semantically similar* (proximity in meaning or difficulty). The framework introduces primitive assumptions characterising:
1. **Prover guarantees** — what a trained prover can prove as a function of graph neighbourhood.
2. **Conjecturer access** — what structural information the conjecturer can observe about $\mathcal{G}$.

### Exponential growth theorem

Under the assumption that $\mathcal{G}$ is *well-connected* (formally: a connectivity or expansion condition on $\mathcal{G}$), a conjecturer that generates new theorems via a **reversible random walk** on $\mathcal{G}$ is sufficient to grow the set of proved theorems exponentially. The intuition: a well-connected graph ensures random walk proposals stay close to the current frontier, keeping them solvable-but-nontrivial; reversibility prevents drift to unreachable regions.

This is the paper's core positive result — a curriculum generation algorithm (random walk on the theorem graph) with provable growth guarantees, without requiring a learned conjecturer reward.

### Diversity measure and improved conjecturing

**Empirical pathology.** Conjecturers trained purely to maximise prover difficulty tend to generate *artificially complex, non-fundamental* theorems — high formal difficulty but low generative value (they don't build toward the breadth of the theorem space).

**Diversity measure.** For a training distribution of conjectured theorems $\mathcal{D}$, diversity is defined using *diffusion similarity* between neighbouring nodes in $\mathcal{G}$:

$$\text{DiffSim}(u, v) = \langle \phi(u), \phi(v) \rangle$$

where $\phi: V \to \mathbb{R}^d$ are embeddings that capture the diffusion distance (random-walk-based proximity) between theorem nodes. A conjecturing distribution that locally maximises this diversity measure is preferred over one that produces near-duplicate or overly-specialised theorems.

**Improved conjecturing algorithm.** The conjecturer is modified to locally maximise the diversity measure — selecting the next conjecture to maximise the diffusion similarity spread among the generated batch, i.e., preferring conjectures that cover diverse regions of $\mathcal{G}$ rather than clustering near already-proved nodes.

### Computing diffusion similarity

Diffusion similarity is approximated by:
1. **Contrastive learning** to embed theorem nodes $\phi(v) \in \mathbb{R}^d$ such that semantically similar theorems are nearby in embedding space.
2. **Inner product** $\langle \phi(u), \phi(v) \rangle$ as the similarity proxy.

This gives a computationally tractable surrogate for the random-walk-based diffusion distance, deployable during training without full graph traversal.

## Results

This is a theory paper — no empirical benchmarks are reported. The main results are:

- **Exponential growth guarantee** for reversible-random-walk conjecturing on well-connected theorem graphs (formal theorem).
- **Diversity measure** characterised as a local objective the conjecturer can optimise to avoid degenerate non-fundamental conjectures.
- **Contrastive embedding** as a practical method to compute diffusion similarity without full graph traversal.

The framework provides theoretical grounding for the Dong & Ma 2025 prover-conjecturer system, and explains two phenomena observed empirically: (1) why a good conjecturer can drive exponential capability growth, and (2) why naive conjecturers collapse to non-useful theorems.

## Connections to the wiki

**Proposer pathology is not new here.** The "artificially complex / non-fundamental conjecture" pathology is the theorem-proving instantiation of a general conjecturer collapse pattern the wiki has documented: [[azr]] avoids it via the solvable-but-not-trivial Goldilocks floor; [[r-zero]] via the symmetric Goldilocks + diversity penalty; [[sqlm]] via the majority-vote frontier gate. The diffusion-similarity diversity measure is a graph-structured analogue of these reward-shaping approaches, but derived theoretically rather than engineered empirically.

**Well-connectedness as the load-bearing assumption.** The exponential growth guarantee depends on $\mathcal{G}$ being well-connected. This is the theorem-proving analogue of the Invisible Leash's "base model capacity" assumption ([[invisible-leash]]): the system can only exponentially expand *within* the connected component it starts in. For formal math, well-connectedness is plausible (Lean's mathlib is densely interconnected); for novel concept learning the analogous graph is far sparser, making the bound less immediately applicable.

**Random walk as a minimal conjecturing strategy.** The sufficiency of a reversible random walk (no learned proposer required) relates to [[two-stage-dynamic]]'s Stage-1/Stage-2 framing: a random-walk proposer provides the curriculum diversity that prevents Stage-1 saturation, even without a high-quality learned proposer. The key is the graph structure, not the sophistication of the proposer model.

**Diversity objective vs. epiplexity.** [[info-gain-self-play]]'s epiplexity criterion ($S_{C,T}(X)$ — the learnable fraction of MDL) and this paper's diffusion-similarity diversity measure address the same failure mode (conjecturer collapse / stagnation) from different angles: epiplexity is an information-theoretic audit of the whole distribution; diffusion similarity is a local geometric objective on the theorem graph. Complementary tools.

## Source

- `raw/research/weekly-2026-06-05/03-self-play-theorem-proving-theory.md`
- arXiv: https://arxiv.org/abs/2606.01861

## Related

- [[_overview]] — self-play theme overview; proposer pathology and the nine reward shapes
- [[azr]] — Goldilocks solvability gate as empirical analogue of the well-connectedness growth condition
- [[r-zero]] — symmetric Goldilocks + diversity penalty; empirical counterpart to diffusion-similarity diversity
- [[sqlm]] — majority-vote frontier gate; cheapest analogue of the conjecture-difficulty targeting
- [[invisible-leash]] — base-model capacity bound; analogous to the well-connectedness assumption
- [[two-stage-dynamic]] — Stage-1/Stage-2 framing; random-walk proposer as a Stage-1 diversity anchor
- [[info-gain-self-play]] — epiplexity as complementary approach to diagnosing conjecturer stagnation
- [[spiral]] — empirical self-play on zero-sum games; diffusion-similarity diversity objective is formally analogous to SPIRAL's multi-game complementarity design
- [[../curriculum-and-decomposition/_overview]] — curriculum learning; conjecturer-as-curriculum-generator is this paper's core architectural frame
- [[../weekly-briefs/2026-06-05]] — brought in by the 2026-06-05 weekly sweep
