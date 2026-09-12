# DATPO: Difficulty-Adaptive Tree-Structured Policy Optimization

DATPO (arXiv:2609.08650, POSTECH) restructures train-time rollouts — difficulty-adaptive tree expansion, sentence-entropy forking, and a sibling-diversity advantage bonus — to expand **pass@k reasoning coverage** rather than just avg@k accuracy. Central argument: rollout *topology*, not just the RL objective, determines whether RLVR unlocks new reasoning paths or merely sharpens existing ones.

## Motivating finding

High rollout budget on *easy* problems causes the model to over-exploit specific, easy templates, degrading pass@256 on hard problems despite avg@256 gains on easy ones (Fig. 1a). Theorem A.2 formalizes this as a **Jensen-gap "variance penalty"** $J_{k,d}(G)$ that scales with cross-prompt dispersion of per-prompt success probability — easy-set training raises this penalty (polarized success: →1 on familiar prompts, →0 on unseen/harder ones) enough to outweigh mean-accuracy gains. This is a quantitative, theory-grounded version of the "RLVR sharpens known solutions rather than discovering new ones" claim already central to the wiki's Invisible Leash line.

## Method

1. **Difficulty-adaptive rollout.** Estimate per-prompt difficulty from base-rollout mean reward $V(root) = \frac{1}{N}\sum_i r(\tau^{(i)})$; scale tree-expansion budget *inversely*: $\hat{K} = \lceil K_{max}(1-V(root)) \rceil$, $\hat{B} = \lceil B_{max}(1-V(root)) \rceil$. Harder prompts get more forking points/branches; $V(root)=1$ (already solved) skips expansion entirely.
2. **Tree rollout** (two-phase). Generate $N$ independent base trajectories; from each, select $K$ forking points and sample $B$ branch continuations per point, sharing the prefix — sub-linear token cost vs. parallel sampling.
3. **Sentence-entropy forking.** Compute token entropy $H_t$, parse into sentences (PySBD), average token entropy per sentence, fork at the top-$K$ highest-entropy *sentences* — avoids "localization," where high-entropy tokens cluster in one narrow segment and token-level forking wastes diversity there.
4. **Block-level diversity-augmented advantage.** Partition trajectories into contiguous blocks at fork points; base advantage via Monte Carlo return $\hat{A}_{base}(b) = r(b) + \hat{V}_{MC}(s_{end}^{(b)}) - \hat{V}_{MC}(s_{start}^{(b)})$. Augment with a sibling-diversity bonus — average cosine distance (gte-large-en-v1.5 embeddings) between block $b$ and its siblings from the same fork point — applied *only* to blocks with positive base advantage (avoids rewarding diversity on wrong paths); the diversity coefficient is linearly annealed to 0 over training (best schedule: 0.2→0).
5. DATPO partitions the tree into **non-overlapping** blocks for updates, so — unlike TreeRL/AttnRL, which flatten the tree into independent sequences and must down-weight shared-prefix advantages by $1/\sqrt{|L(s_n)|}$ as an ad-hoc fix — it never double-updates on duplicated prefixes.

## Results

Qwen2.5-3B-Base and Qwen3-4B-Base trained on MATH (12k problems), evaluated on MATH500/AIME24/25/26/AMC23 against Base, GRPO+DAPO tricks, Dr.GRPO, TreeRL, and AttnRL:

- Best *average* avg@k and pass@k of all baselines. avg@k gains over best baseline (AttnRL) are marginal (+1.1/+0.6pp), but **pass@k gains are large**: +1.9pp (3B: 54.9 vs. 53.0) and +3.0pp (4B: 60.4 vs. 57.4).
- Wide margins on AIME24/25 pass@64 (4B AIME24 pass@64: 46.7 vs. 42.2 AttnRL, 41.1 GRPO).
- maj@k test-time-scaling gain over avg@k is largest for DATPO (+7.2) vs. GRPO/Dr.GRPO/TreeRL/AttnRL (+5.9/+4.6/+4.5/+6.2) — train-time pass@k gains transfer to test-time maj@k.
- DATPO's MATH500 accuracy keeps climbing over 700 steps while TreeRL/AttnRL plateau or regress, attributed to the annealed diversity bonus preventing premature convergence.
- Forking-strategy ablation: sentence-entropy forking gets the best PassRate (17.3) with near-best sibling diversity (0.1049); token-entropy forking has higher diversity (0.1065) but suffers localization, giving the worst PassRate among diverse methods (12.0).

## Limitations (author-acknowledged)

- Sibling-diversity bonus requires extra forward passes through an external embedding model — compute overhead.
- Small rollout counts ($N=4, B=4$) for difficulty/MC-value estimation inject noise into policy updates.
- Only validated at 3B–4B scale; scalability to ≥7B unverified.
- Math-only evaluation; generalization to logic or code untested.
- Unstated: the difficulty estimator $V(root)$ is a noisy Monte Carlo mean, recomputed fresh every step with no smoothing.

## Relation to other wiki entries

- Theorem A.2's variance-penalty account of pass@k is a formal companion to [[binary-rewards-rl-challenges]]'s I-projection collapse account and the Invisible Leash line's "RLVR sharpens known solutions" claim (see [[../self-play/_overview]]).
- Difficulty-adaptive rollout allocation directly parallels [[../curriculum-and-decomposition/pac-progress-augmented-curriculum]]'s Bayesian Thompson-sampling rollout-budget curriculum — same design question (allocate rollout compute by difficulty) via a different mechanism (per-prompt reward-based estimate vs. cross-task Bayesian sampling).
- The block-level diversity-augmented advantage is comparable to [[../rl-optimizers/_overview]]'s pass@k-targeting advantage-modification methods (e.g. VPO's Dirichlet-sampled scalarizations) — DATPO uses embedding-cosine sibling diversity for the same coverage goal.
- DATPO is positioned against TreeRL (Hou et al. 2025) and AttnRL (Liu et al. 2025a) — first wiki appearance of that tree-rollout lineage.

## Source

- arXiv: [2609.08650](https://arxiv.org/abs/2609.08650) — "Difficulty-Adaptive Tree-Structured Policy Optimization for Expanding Reasoning Coverage in RLVR"
- Captured via 2026-09-11 weekly sweep: `raw/research/weekly-2026-09-11/05-difficulty-adaptive-tree-rlvr.md`

## Related

- [[_overview]] — rlvr-mechanics theme overview
- [[binary-rewards-rl-challenges]] — companion information-geometric account of diversity collapse
- [[../curriculum-and-decomposition/pac-progress-augmented-curriculum]] — parallel adaptive rollout-budget curriculum, different mechanism
- [[../curriculum-and-decomposition/_overview]] — curriculum theme, difficulty-allocation thread
- [[../self-play/_overview]] — Invisible Leash proposer-quality anchor; DATPO's easy-data finding is a quantitative instance of the same pattern
- [[../rl-optimizers/_overview]] — pass@k/coverage-targeting advantage-modification methods
- [[../../weekly-briefs/2026-09-11]] — brought in by the 2026-09-11 weekly sweep
