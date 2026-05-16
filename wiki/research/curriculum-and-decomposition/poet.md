# Paired Open-Ended Trailblazer (POET): Endlessly Generating Increasingly Complex and Diverse Learning Environments and Their Solutions

Wang, Lehman, Clune, and Stanley present an algorithm that co-evolves environments and agents: given a simple starting task, POET mutates environments to create new challenges, optimizes agents to solve them, and transfers successful policies between environments when beneficial. This open-ended process automatically discovers a curriculum of stepping-stone problems and corresponding solutions, with no predetermined target. (arXiv:1901.01753, 2019)

## Method

POET maintains a population of environment-agent pairs. At each iteration, it performs three operations: (1) **environment generation** via random mutation of active environments' parameter vectors (obstacle types: stump height, gap width, step height, step count, roughness), conditioned on reproducibility (the paired agent must score ≥200) and a novelty-based filter (minimal-criterion: accept new environments only if neither too easy nor too hard for current agents); (2) **agent optimization** via evolutionary strategies (ES), where each agent is optimized independently within its paired environment; (3) **transfer attempts**, where agents from one environment are tested in others—if an agent from environment B outperforms the current agent in environment A, it replaces it.

The minimal-criterion + novelty-search combination ensures that new environments form genuine stepping stones rather than random noise. The system implicitly builds multiple overlapping curricula simultaneously because new environments are mutations of solved ones, creating ancestor chains. Critically, transfer unlocks serendipitous cross-environment solutions: an agent stuck in a local optimum in one environment may be rescued by a successful strategy evolved elsewhere, reflecting the idea that "the most promising stepping stone to the best possible outcome may not be the current top performer in that environment" (Sec. 3).

## Claims

- **Solves unsolvable problems**: POET generates and solves environments that direct ES optimization cannot, even when ES is given twice the typical budget (16,000 steps). For example, wide-gap crossing and oversized staircase environments yield ES max scores of 13.6–39.6 vs. POET's success threshold of 230+ (Figs. 2–3, Sec. 4.2).

- **Diverse environment generation**: Figure 5 and supplemental figures show that POET creates obstacles spanning wide ranges—e.g., gap widths from 0.5 to 8.0, stump heights from 0.5 to 3.0, roughness from 0 to 8—all within a single run, with individual environments specializing in different obstacle combinations (Figs. 5, 9).

- **Outperforms explicit curricula**: A direct-path curriculum-building control (incrementally increasing difficulty toward a target) fails to reach very and extremely challenging POET-generated targets; Mann–Whitney U tests show significant gaps (p < 0.01) between challenge levels, demonstrating that single-chain curricula cannot match the frontier achieved by multi-path co-evolution (Figs. 5–6, Sec. 4.2).

- **Stepping-stone transfer is essential**: A control run of POET without transfer generates no extremely challenging environments (Fig. 8), proving that cross-environment transfer is critical to unlocking the full divergent potential of the system.

- **Automatic curriculum**: POET implicitly self-generates multiple curricula because new environments are mutations of parents and must not be too easy/hard for agents, creating a smooth progression along many parallel paths (Sec. 4.2, Discussion).

- **Computational efficiency via parallelization**: The independence of agent optimization and transfer attempts across environment-agent pairs enables seamless distribution across 256 CPU cores without synchronization (Sec. 3).

## Relevance to the project

**Structural analogy (a)**: RCL's co-discovery of (prerequisite concept, student capability) mirrors POET's co-evolution of (environment, agent). In POET, environments are parameterized obstacles that grow in complexity; in RCL, concepts are natural-language learning goals. Both systems let the curriculum emerge: POET through mutation + novelty filtering, RCL through observed student mastery patterns and prerequisite decomposition. Neither pre-specifies a target curriculum.

**Transfer as prerequisite check (b)**: POET's transfer step—testing whether an agent from one environment solves another—directly parallels RCL's implicit question: "Did training on prerequisite concept c1 unlock parent concept c?" Both use transfer success as a signal of stepping-stone utility. The minimal-criterion (accept new environment only if solvable by current agents) is analogous to RCL checking whether a discovered prerequisite is actually learnable given current student state.

**Key differences (c)**: POET's environments are low-dimensional real vectors (obstacle parameters); RCL's concepts are natural-language descriptions requiring semantic decomposition. POET uses random mutation + statistical filtering (minimal-criterion + novelty); RCL uses M.Decompose, a goal-directed goal decomposer that selects *semantic* prerequisites. POET has no diagnostic teacher—it cannot ask "why did this environment fail?"—whereas RCL's decomposer actively reasons about learning bottlenecks. This difference reflects RCL's emphasis on interpretability and human-guided concept hierarchies versus POET's pure emergent search. However, the core principle—that stepping-stone solutions transfer between tasks and that a curriculum need not be hand-crafted—is identical.

## Source

- arXiv: 1901.01753
- Authors: Rui Wang, Joel Lehman, Jeff Clune, Kenneth O. Stanley
- Year: 2019
- Raw markdown: `../../../raw/research/rcl-gap-fillers/06-poet.md`

## Related

- [[_overview]] — curriculum-and-decomposition theme overview
- [[options-framework]] — sibling on hierarchical/emergent structure; POET emerges environments, options framework abstracts over them
- [[acl-deep-rl-survey]] — POET is one of the canonical ACL methods catalogued in the survey
- [[../synthesis/recursive-concept-learning]] — closest spirit-match to RCL's failure-driven lazy DAG expansion; POET's transfer-attempt step is the structural analogue of "did training prereq c1 unlock parent c?"
- [[../teacher-student-rl/soar-edge-of-learnability]] — bilevel meta-RL where teacher reward = student improvement; same loop shape as POET's environment/agent co-evolution at the curriculum scale
- [[../concept-learning/recursive-concept-evolution]] — RCE's spawn-on-failure + MDL-on-accept is POET's mutation + minimal-criterion filter, lifted to the concept-library level
